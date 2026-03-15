import numpy as np
import tensorflow as tf
import keras
from scipy.io import wavfile
import librosa
import os

MODEL_PATH = 'static/models/alien_model.h5'  # Сохранить сюда из DataSphere

model = None

def load_model():
    global model
    if model is None and os.path.exists(MODEL_PATH):
        model = keras.models.load_model(MODEL_PATH)
    return model

def preprocess_wav(wav_data, sr=16000):
    # Пример: MFCC features
    mfccs = librosa.feature.mfcc(y=wav_data.astype(float), sr=sr, n_mfcc=13)
    mfccs = np.mean(mfccs.T, axis=0)
    return np.expand_dims(mfccs, axis=0)

def predict_dataset(npz_path):
    data = np.load(npz_path)
    test_x = data['test_x']  # wav bytes or paths?
    test_y = data['test_y']
    
    load_model()
    if model is None:
        raise ValueError("Model not loaded")
    
    predictions = []
    accuracies = []
    for i, wav_bytes in enumerate(test_x):
        sr, wav_data = wavfile.read(wav_bytes) if isinstance(wav_bytes, bytes) else (16000, wav_bytes)
        features = preprocess_wav(wav_data, sr)
        pred = model.predict(features)
        pred_class = np.argmax(pred)
        accuracy = 1 if pred_class == test_y[i] else 0
        predictions.append(pred_class)
        accuracies.append(accuracy)
    
    overall_acc = np.mean(accuracies)
    return predictions, test_y, overall_acc

def get_training_analytics(npz_train_path='train_valid.npz'):
    # Заглушки для аналитики - заменить на реальные из обучения
    data = np.load(npz_train_path)
    train_y = data['train_y']
    
    # График accuracy vs epochs (заглушка)
    epochs = list(range(1, 51))
    accuracy = [0.1 + 0.7 * (1 - np.exp(-i/10)) for i in epochs]
    
    # Диаграмма классов train
    unique, counts = np.unique(train_y, return_counts=True)
    
    # Accuracy per test sample (заглушка)
    test_acc = np.random.choice([0,1], 400)
    
    # Top-5 valid classes
    valid_y = data['valid_y']
    valid_top5 = np.unique(valid_y, return_counts=True)[1][:5]
    
    return {
        'epochs': epochs,
        'accuracy': accuracy,
        'train_classes': dict(zip(unique, counts)),
        'test_acc': test_acc,
        'valid_top5': valid_top5
    }
