import chromadb

client=chromadb.PersistentClient(path='chroma_db')

collection=client.get_collection(name='vaultx_docs')

print(f'Total items in collection: {collection.count()}')