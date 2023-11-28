import spacy
import fitz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ruta al modelo de SpaCy (ajustar según sea necesario)
MODEL_PATH = r'apis/Modelo4/output/model-best'

# Inicializar el modelo de SpaCy
nlp_model = spacy.load(MODEL_PATH)

# Inicializar el vectorizador CountVectorizer
cv = CountVectorizer()

def preprocess_text(text):
    return ' '.join(text.strip().split())

def load_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_resume(pdf_path):
    # Cargar el texto del currículum desde el archivo PDF
    #resume_text = load_text_from_pdf(pdf_path)
    resume_text = pdf_path

    # Preprocesar el texto
    resume_text = preprocess_text(resume_text)

    # Procesar el texto con el modelo de SpaCy
    doc = nlp_model(resume_text)
    entities = [{'label': ent.label_, 'text': ent.text} for ent in doc.ents]

    return entities

def calculate_similarity(resume_path, job_description_path):
    # Cargar textos desde archivos PDF
    #resume_text = load_text_from_pdf(resume_path)
    resume_text = resume_path
    #job_description_text = load_text_from_pdf(job_description_path)
    job_description_text = job_description_path

    # Preprocesar textos
    resume_text = preprocess_text(resume_text)
    #job_description_text = preprocess_text(job_description_text)

    # Calcular similitud entre el currículum y la descripción del trabajo
    match = [resume_text, job_description_text]
    count_matrix = cv.fit_transform(match)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    match_percentage = round(match_percentage, 2)

    return match_percentage

# Ejemplo de uso de las funciones
if __name__ == "__main__":
    # Rutas de archivos PDF (ajustar según sea necesario)
    resume_pdf_path = r'D:/ResumenCVtest//Alice Clark CV.pdf'
    job_description_pdf_path = r'D:/ResumenCV/test/pythonJobDescription.pdf'

    # Procesar el currículum
    entities = process_resume(resume_pdf_path)
    print("Entidades en el currículum:", entities)

    # Calcular la similitud entre el currículum y la descripción del trabajo
    similarity_percentage = calculate_similarity(resume_pdf_path, job_description_pdf_path)
    print("El currículum tiene un porcentaje del {}% de similitud para el puesto de trabajo".format(similarity_percentage))
