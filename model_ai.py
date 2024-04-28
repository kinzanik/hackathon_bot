import torch
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import torch.nn as nn
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('puntk')
nltk.download('stopwords')

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Предположим, что input_size и output_size известны из вашего обучения модели
input_size = 270  # Замените это на реальное значение
output_size = 30  # Замените это на реальное значение

# Создание экземпляра модели
model = NeuralNetwork(input_size, output_size)


model.load_state_dict(torch.load('model.pth'))
model.eval()  # Установите модель в режим оценки



train_data = pd.read_csv('train_SecondPilot/train_data.csv')

# Fill missing values in the 'Question' column with an empty string
train_data['Question'].fillna('', inplace=True)

# Get the text data from the 'Question' column
X_train = train_data['Question']

# Initialize the CountVectorizer
vectorizer = CountVectorizer()

# Fit the vectorizer on the text data
vectorizer.fit(X_train)

# Transform the text data into a numerical representation
X_train_vectorized = vectorizer.transform(X_train)

# Convert the sparse matrix to a dense numpy array
X_train_dense = X_train_vectorized.toarray()

# Print the shape of X_train_dense for verification
print("Shape of X_train_dense:", X_train_dense.shape)

def preprocess_question(question):
    question_vectorized = vectorizer.transform([question])
    return question_vectorized.toarray()[0]


def predict_answer(question):
    # Предобработка вопроса
    processed_question = preprocess_question(question)

    # Преобразование вопроса в тензор PyTorch
    X_question_tensor = torch.tensor(processed_question, dtype=torch.float32)

    # Получение предсказанного класса от модели
    output = model(X_question_tensor.unsqueeze(0))  # Добавляем размерность пакета (batch dimension)
    predicted_class = torch.argmax(output).item()

    # Декодирование предсказанного класса (если необходимо)
    # Здесь вы можете выполнить обратное преобразование, если использовали кодирование меток
    # decoded_answer = label_encoder.inverse_transform([predicted_class])[0]

    # Возвращение предсказанного класса или ответа
    return predicted_class


answer_class_data = pd.read_csv('train_SecondPilot/answer_class.csv')


# Функция для получения текста ответа по предсказанному классу
def get_answer_text(predicted_class):
    answer_text = answer_class_data.loc[answer_class_data['answer_class'] == predicted_class, 'Answer'].values[0]
    return answer_text


# Функция для предсказания ответа на вопрос с текстом ответа
def predict_answer_with_text(question):
    # Предобработка вопроса и предсказание класса
    predicted_class = predict_answer(question)

    # Получение текста ответа по предсказанному классу
    answer_text = get_answer_text(predicted_class)

    return answer_text


if __name__ == '__main__':

    question = "Как дела"
    answer_text = predict_answer_with_text(question)
    print("Предсказанный ответ:", answer_text)