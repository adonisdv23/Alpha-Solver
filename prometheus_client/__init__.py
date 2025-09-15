from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"


class CollectorRegistry:
    """Very small in-memory collector compatible with the real API subset."""

    def __init__(self) -> None:
        self._metrics: List[_Metric] = []
        self._collector_to_names: Dict[_Metric, Set[str]] = {}
        self._names_to_collectors: Dict[str, Set[_Metric]] = {}

    def register(self, metric: "_Metric") -> None:
        if metric not in self._metrics:
            self._metrics.append(metric)
        previous = self._collector_to_names.get(metric, set())
        for name in previous:
            collectors = self._names_to_collectors.get(name)
            if collectors is None:
                continue
            collectors.discard(metric)
            if not collectors:
                del self._names_to_collectors[name]
        names = set(metric._sample_names())
        self._collector_to_names[metric] = names
        for name in names:
            self._names_to_collectors.setdefault(name, set()).add(metric)

    def collect(self) -> List["_CollectedMetric"]:
        collected: List[_CollectedMetric] = []
        for metric in self._metrics:
            if metric not in self._collector_to_names:
                continue
            collected.append(metric._collect())
        return collected

    def get_sample_value(
        self,
        name: str,
        labels: Optional[Dict[str, Any]] = None,
    ) -> Any:
        for metric in self._metrics:
            if metric not in self._collector_to_names:
                continue
            value = metric.get_sample_value_from_name(name, labels)
            if value is not None:
                return value
        return None


_DEFAULT_REGISTRY = CollectorRegistry()
REGISTRY = _DEFAULT_REGISTRY


class _Sample:
    def __init__(self, metric: "_Metric", key: Tuple[Any, ...]):
        self._metric = metric
        self._key = key

    def inc(self, amount: float = 1.0) -> None:
        self._metric._inc_value(self._key, amount)

    def dec(self, amount: float = 1.0) -> None:
        self._metric._inc_value(self._key, -amount)

    def observe(self, value: float) -> None:
        self._metric._observe_sample(self._key, value)

    def set(self, value: float) -> None:
        self._metric._set_value(self._key, value)


class _Metric:
    def __init__(
        self,
        name: str,
        documentation: str = "",
        labelnames: Optional[Iterable[str]] = None,
        *,
        registry: Optional[CollectorRegistry] = None,
    ) -> None:
        self.name = name
        self.documentation = documentation
        if labelnames is None:
            self._labelnames = ()
        elif isinstance(labelnames, (list, tuple)):
            self._labelnames = tuple(labelnames)
        elif isinstance(labelnames, str):
            self._labelnames = (labelnames,)
        else:
            self._labelnames = tuple(labelnames)
        self._samples: Dict[Tuple[Any, ...], float] = {}
        if not self._labelnames:
            self._samples[()] = 0.0
        self._registry = registry or _DEFAULT_REGISTRY
        self._registry.register(self)

    @property
    def labelnames(self) -> Tuple[str, ...]:
        return self._labelnames

    def _key_from_labels(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Tuple[Any, ...]:
        if not self._labelnames:
            if args or kwargs:
                raise ValueError("Metric has no labels")
            return ()
        if args and kwargs:
            raise ValueError("Specify labels either positionally or by name")
        if args:
            if len(args) != len(self._labelnames):
                raise ValueError("Incorrect number of labels")
            return tuple(args)
        values = []
        for name in self._labelnames:
            if name not in kwargs:
                raise ValueError(f"Missing label: {name}")
            values.append(kwargs[name])
        if len(kwargs) != len(self._labelnames):
            extra = set(kwargs) - set(self._labelnames)
            if extra:
                raise ValueError(f"Unexpected labels: {sorted(extra)}")
        return tuple(values)

    def labels(self, *args: Any, **kwargs: Any) -> _Sample:
        key = self._key_from_labels(args, kwargs)
        if key not in self._samples:
            self._samples[key] = 0.0
        return _Sample(self, key)

    def _inc_value(self, key: Tuple[Any, ...], amount: float) -> None:
        self._samples[key] = float(self._samples.get(key, 0.0)) + float(amount)

    def _set_value(self, key: Tuple[Any, ...], value: float) -> None:
        self._samples[key] = float(value)

    def _observe_sample(self, key: Tuple[Any, ...], value: float) -> None:
        self._set_value(key, value)

    def get_sample_value(self, labels: Optional[Dict[str, Any]] = None) -> Any:
        if not self._labelnames:
            return self._samples.get(())
        if labels is None:
            return None
        if isinstance(labels, dict):
            try:
                key = tuple(labels[name] for name in self._labelnames)
            except KeyError:
                return None
        elif isinstance(labels, (list, tuple)):
            if len(labels) != len(self._labelnames):
                return None
            key = tuple(labels)
        else:
            return None
        return self._samples.get(key)

    def get_sample_value_from_name(
        self, name: str, labels: Optional[Dict[str, Any]] = None
    ) -> Any:
        if name == self.name:
            return self.get_sample_value(labels)
        return None

    def _sample_name(self) -> str:
        return self.name

    def _sample_names(self) -> Iterable[str]:
        yield self._sample_name()

    def _iter_samples(self) -> Iterable[Tuple[str, Tuple[Any, ...], float]]:
        for key, value in self._samples.items():
            yield self._sample_name(), key, value

    def _metric_name(self) -> str:
        return self.name

    def _collect(self) -> "_CollectedMetric":
        samples = []
        for sample_name, labels, value in self._iter_samples():
            label_map = (
                dict(zip(self.labelnames, labels)) if self.labelnames else {}
            )
            samples.append(_CollectedSample(sample_name, label_map, value))
        return _CollectedMetric(self._metric_name(), samples)

    # default implementations for unlabeled variants -----------------
    def inc(self, amount: float = 1.0) -> None:
        if self._labelnames:
            raise ValueError("Use labels().inc() on labelled metrics")
        self._inc_value((), amount)

    def observe(self, value: float) -> None:
        if self._labelnames:
            raise ValueError("Use labels().observe() on labelled metrics")
        self._set_value((), value)

    def set(self, value: float) -> None:
        if self._labelnames:
            raise ValueError("Use labels().set() on labelled metrics")
        self._set_value((), value)


class Counter(_Metric):
    def __init__(
        self,
        name: str,
        documentation: str = "",
        labelnames: Optional[Iterable[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        registry = kwargs.pop("registry", None)
        super().__init__(name, documentation, labelnames, registry=registry)

    def _sample_name(self) -> str:
        if self.name.endswith("_total"):
            return self.name
        return f"{self.name}_total"

    def _sample_names(self) -> Iterable[str]:
        yield self._sample_name()

    def _metric_name(self) -> str:
        if self.name.endswith("_total"):
            return self.name[: -len("_total")]
        return self.name

    def get_sample_value_from_name(
        self, name: str, labels: Optional[Dict[str, Any]] = None
    ) -> Any:
        if name == self._sample_name():
            return self.get_sample_value(labels)
        return super().get_sample_value_from_name(name, labels)


class Gauge(_Metric):
    def __init__(
        self,
        name: str,
        documentation: str = "",
        labelnames: Optional[Iterable[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        registry = kwargs.pop("registry", None)
        super().__init__(name, documentation, labelnames, registry=registry)

    def dec(self, amount: float = 1.0) -> None:
        if self.labelnames:
            raise ValueError("Use labels().dec() on labelled metrics")
        self._inc_value((), -amount)


class Histogram(_Metric):
    def __init__(
        self,
        name: str,
        documentation: str = "",
        labelnames: Optional[Iterable[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        registry = kwargs.pop("registry", None)
        buckets = kwargs.pop("buckets", None)
        super().__init__(name, documentation, labelnames, registry=registry)
        self._samples.clear()
        processed = [float(b) for b in buckets] if buckets is not None else []
        processed.sort()
        if not processed or processed[-1] != float("inf"):
            processed.append(float("inf"))
        self._buckets = processed
        self._bucket_counts: Dict[Tuple[Any, ...], List[float]] = {}
        self._sum: Dict[Tuple[Any, ...], float] = {}
        self._count: Dict[Tuple[Any, ...], int] = {}

    def _ensure_state(self, key: Tuple[Any, ...]) -> None:
        if key in self._bucket_counts:
            return
        self._bucket_counts[key] = [0.0 for _ in self._buckets]
        self._sum[key] = 0.0
        self._count[key] = 0

    def _observe_sample(self, key: Tuple[Any, ...], value: float) -> None:
        self._ensure_state(key)
        self._sum[key] += float(value)
        self._count[key] += 1
        for idx, bound in enumerate(self._buckets):
            if float(value) <= bound:
                self._bucket_counts[key][idx] += 1

    def _sample_names(self) -> Iterable[str]:
        yield f"{self.name}_bucket"
        yield f"{self.name}_sum"
        yield f"{self.name}_count"

    def _collect(self) -> "_CollectedMetric":
        samples: List[_CollectedSample] = []
        if not self._bucket_counts and not self.labelnames:
            self._ensure_state(())
        for key, counts in self._bucket_counts.items():
            base_labels = (
                dict(zip(self.labelnames, key)) if self.labelnames else {}
            )
            for bound, count in zip(self._buckets, counts):
                labels = base_labels.copy()
                labels["le"] = "+Inf" if bound == float("inf") else str(bound)
                samples.append(
                    _CollectedSample(f"{self.name}_bucket", labels, count)
                )
            samples.append(
                _CollectedSample(
                    f"{self.name}_count",
                    base_labels.copy(),
                    self._count.get(key, 0),
                )
            )
            samples.append(
                _CollectedSample(
                    f"{self.name}_sum",
                    base_labels.copy(),
                    self._sum.get(key, 0.0),
                )
            )
        return _CollectedMetric(self._metric_name(), samples)

    def get_sample_value_from_name(
        self, name: str, labels: Optional[Dict[str, Any]] = None
    ) -> Any:
        if name == f"{self.name}_sum":
            key = self._labels_to_key(labels)
            if key is None:
                return None
            return self._sum.get(key)
        if name == f"{self.name}_count":
            key = self._labels_to_key(labels)
            if key is None:
                return None
            return self._count.get(key)
        if name == f"{self.name}_bucket":
            if labels is None or "le" not in labels:
                return None
            le = labels["le"]
            key_labels = {k: v for k, v in labels.items() if k != "le"}
            key = self._labels_to_key(key_labels)
            if key is None:
                return None
            if le == "+Inf":
                bound = float("inf")
            else:
                try:
                    bound = float(le)
                except (TypeError, ValueError):
                    return None
            self._ensure_state(key)
            for idx, bucket_bound in enumerate(self._buckets):
                if bucket_bound == bound:
                    return self._bucket_counts[key][idx]
            return None
        return super().get_sample_value_from_name(name, labels)

    def _labels_to_key(self, labels: Optional[Dict[str, Any]]) -> Optional[Tuple[Any, ...]]:
        if not self.labelnames:
            return ()
        if labels is None:
            return None
        try:
            return tuple(labels[name] for name in self.labelnames)
        except KeyError:
            return None


class _CollectedSample:
    def __init__(self, name: str, labels: Dict[str, Any], value: float) -> None:
        self.name = name
        self.labels = labels
        self.value = value


class _CollectedMetric:
    def __init__(self, name: str, samples: List[_CollectedSample]) -> None:
        self.name = name
        self.samples = samples


def generate_latest(registry: Optional[CollectorRegistry] = None) -> bytes:
    registry = registry or _DEFAULT_REGISTRY
    lines = []
    for metric in registry.collect():
        for sample in metric.samples:
            if sample.labels:
                parts = [f'{key}="{value}"' for key, value in sample.labels.items()]
                lines.append(f"{sample.name}{{{','.join(parts)}}} {sample.value}")
            else:
                lines.append(f"{sample.name} {sample.value}")
    return "\n".join(lines).encode()


def start_http_server(port: int) -> None:  # pragma: no cover - noop
    return None


__all__ = [
    "CollectorRegistry",
    "Counter",
    "Gauge",
    "Histogram",
    "REGISTRY",
    "CONTENT_TYPE_LATEST",
    "generate_latest",
    "start_http_server",
]
