import os
import json
# 设置文件夹的基础路径
# AST_path = 'Dive_AST'  # 替换为您的主文件夹路径 
# AST_base='ast.dot'

# CFG_path = 'Dive_CFG'  # 替换为您的主文件夹路径
# CFG_base='cfg.dot'

# PDG_path = 'Dive_PDG'  # 替换为您的主文件夹路径
# PDG_base='pdg.dot'

CPG_path = 'Dive_CPG'  # 替换为您的主文件夹路径
CPG_base='cpg.dot/temp.c'

def combine(base_path,base):
    # 遍历3200个文件夹
    for i in range(1, 32001):
        folder_path = os.path.join(base_path, str(i), base)
        
        # 确认ast.dot子文件夹是否存在
        if os.path.exists(folder_path):
            with open(os.path.join(folder_path, 'combine.dot'), 'w') as outfile:
                # 遍历ast.dot文件夹中的所有.dot文件
                for filename in os.listdir(folder_path):
                    if filename.endswith('.dot') and filename != 'combine.dot':
                        with open(os.path.join(folder_path, filename), 'r') as infile:
                            # 将文件内容写入combine.dot
                            outfile.write(infile.read() + '\n')  # 将文件之间用换行符分隔

# combine(AST_path,AST_base)   
# print("AST合并完成!") 
# combine(CFG_path,CFG_base)   
# print("CFG合并完成!") 
# combine(PDG_path,PDG_base)   
# print("PDG合并完成!") 
combine(CPG_path,CPG_base)   
print("CPG合并完成!") 


# AST_output_file = 'AST_combined.jsonl'
# CFG_output_file = 'CFG_combined.jsonl'
# PDG_output_file = 'PDG_combined.jsonl'
CPG_output_file = 'CPG_combined.jsonl'
def Conver_Jsonl(base_path,base,output_file):
    data = []
    # 遍历3200个文件夹
    for i in range(1, 32001):
        folder_path = os.path.join(base_path, str(i), base)
        combine_file_path = os.path.join(folder_path, 'combine.dot')
        
        if os.path.exists(combine_file_path):
            with open(combine_file_path, 'r') as file:
                content = file.read()
                data.append({"func": content})

    # 将数据写入jsonl文件
    with open(output_file, 'w') as outfile:
        for entry in data:
            outfile.write(json.dumps(entry) + '\n')

    

# Conver_Jsonl(AST_path,AST_base,AST_output_file)
# print("完成转换到AST_JSONL!")
# Conver_Jsonl(CFG_path,CFG_base,CFG_output_file)
# print("完成转换到CFG_JSONL!")
# Conver_Jsonl(PDG_path,PDG_base,PDG_output_file)
# print("完成转换到PDG_JSONL!")
Conver_Jsonl(CPG_path,CPG_base,CPG_output_file)
print("完成转换到CPG_JSONL!")

label_file = 'Label.jsonl'
# Label_AST_output_file = 'Label_AST_combined.jsonl'
# Label_CFG_output_file = 'Label_CFG_combined.jsonl'
# Label_PDG_output_file = 'Label_PDG_combined.jsonl'
Label_CPG_output_file = 'Label_CPG_combined.jsonl'

def add_Label(combined_file,output_file):
    with open(combined_file, 'r') as cfile, open(label_file, 'r') as lfile, open(output_file, 'w') as ofile:
        for cline, lline in zip(cfile, lfile):
            combined_data = json.loads(cline)
            label_data = json.loads(lline)
            
            merged_data = {
                "target": label_data["target"],
                "func": combined_data["func"]
            }
        
            ofile.write(json.dumps(merged_data) + '\n')
            
# add_Label('AST_combined.jsonl','Label_AST_combined.jsonl')
# print("AST_合并完成!")
# add_Label('CFG_combined.jsonl','Label_CFG_combined.jsonl') 
# print("CFG_合并完成!")   
# add_Label('PDG_combined.jsonl','Label_PDG_combined.jsonl')
# print("PDG_合并完成!")              
add_Label('CPG_combined.jsonl','Label_CPG_combined.jsonl')
print("CPG_合并完成!")         
