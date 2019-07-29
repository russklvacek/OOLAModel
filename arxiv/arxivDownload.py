import arxiv

results = arxiv.query(query="learning analytics education", max_results=1000)
print("Found ", len(results), " papers.")
#print(results)
for paper in results:
    print("Downloading: ", paper['title'], " ", paper['published'])
    #arxiv.download(paper)