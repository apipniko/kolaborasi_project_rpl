import pickle

with open('kolaborasi_project_rpl\models\model_rekomendasi.pkl', 'rb') as file:
    model_data = pickle.load(file)

print(type(model_data))
print("Isi dari model ini adalah:")
print(model_data.keys())