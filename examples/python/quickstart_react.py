from clients.python.alpha_client import AlphaClient

client = AlphaClient("http://localhost:8000", "changeme")
result = client.solve("Explain 2+2", strategy="react", context={"seed": 1337})
print(result["final_answer"], result["confidence"])
