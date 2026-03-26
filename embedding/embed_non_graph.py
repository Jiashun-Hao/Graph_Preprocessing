import json
import gensim.models.doc2vec as doc2vec
from gensim.models.doc2vec import TaggedDocument
def Embeding(Jsonl_path,output_Jsonl):
    # Define the Doc2Vec model
    model = doc2vec.Doc2Vec(vector_size=100, window=5, min_count=1, workers=4)
    # Function to parse JSONL file and preprocess data
    def parse_jsonl(file_path):
        documents = []
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                content = data['func']
                if isinstance(content, dict):
                    content = json.dumps(content)  # Convert nested dict to string
                documents.append(TaggedDocument(words=content.split(), tags=[data['target']]))
            print("Run1...")    
        return documents

    print("Run0...")
    # Load and preprocess data from the JSONL file

    #documents = parse_jsonl('Label_PDG_combined.jsonl')
    documents = parse_jsonl(Jsonl_path)

    # Build the vocabulary
    model.build_vocab(documents)

    # Train the Doc2Vec model
    model.train(documents, total_examples=model.corpus_count, epochs=50)

    # Function to convert 'func' field to Doc2Vec vectors
    def convert_func_to_vectors(file_path, model, output_file):
        with open(file_path, 'r') as input_file, open(output_file, 'w') as output_file:
            for line in input_file:
                data = json.loads(line.strip())
                content = data['func']
                if isinstance(content, dict):
                    content = json.dumps(content)  # Convert nested dict to string
                vec = model.infer_vector(content.split())
                data['func'] = vec.tolist()
                output_file.write(json.dumps(data) + '\n')
                print("Run2...")

    # Convert 'func' field to Doc2Vec vectors and save to new JSONL file
    # convert_func_to_vectors('Label_PDG_combined.jsonl', model, 'PDG_Emberding_code.jsonl')
    convert_func_to_vectors(Jsonl_path, model, output_Jsonl)

# Embeding('Label_PDG_combined.jsonl','PDG_Emberding_code.jsonl')
# print("PDG_ok")
# Embeding('Label_AST_combined.jsonl','AST_Emberding_code.jsonl')
# print("AST_ok")
# Embeding('Label_CFG_combined.jsonl','CFG_Emberding_code.jsonl')
# print("CFG_ok")
Embeding('Label_CPG_combined.jsonl','CPG_Emberding_code.jsonl')
print("CPG_ok")