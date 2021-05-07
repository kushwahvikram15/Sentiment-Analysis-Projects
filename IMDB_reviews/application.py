from tkinter import *
from PIL import ImageTk,Image
from tkinter.font import Font
import tkinter
import pickle
from PIL.ImageTk import PhotoImage
import pandas as pd
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
class IMDB():
    def __init__(self,root):
        self.master = root
        self.img = ImageTk.PhotoImage(Image.open("C:\\Users\\vikra\\Desktop\\lat.jpg"))
        self.f = Frame(self.master, height=self.master.winfo_screenwidth(), width=self.master.winfo_screenwidth())
        self.f.place(x=0, y=0)
        self.l = Label(self.f, image=self.img)
        self.l.place(x=0, y=0)
        self.myfont = Font(family='Ink Free', size=15, weight='bold')
        self.button2 = Button(self.f, text="Enter Text", height=3, width=40, bg='grey', command=self.text).place(x=650, y=580)

    def text(self):
        self.w = Text(self.f, height=7, width=70, bg='#272f3b', font=self.myfont, fg='white')
        self.w.place(x=400, y=200)
        self.button1 = Button(self.f, text="Get Result", height=3, width=40, bg='grey', command=self.retrieve_input)
        self.button1.place(x=650, y=580)

    def retrieve_input(self):
        self.input = self.w.get("1.0", END)
        self.w.destroy()
        self.button1.destroy()
        self.result_frame = Frame(self.f, height=500, width=500, bg='#2e2b2b')
        self.result_frame.place(x=500, y=180)
        self.button3 = Button(self.result_frame, text="Back", height=1, width=5, bg='grey', command=self.back)
        self.button3.place(x=450, y=5)

        self.result = self.generate_result()
        if self.result[0]==1:
            file = 'up.png'
            text = 'This Review is good.'
        else:
            file = 'down.png'
            text = "This Review is Bad"
        self.icon = PhotoImage(file=file)
        self.logolbl = Label(self.result_frame, image=self.icon, bd=0, bg='#2e2b2b')
        self.logolbl.place(x=100, y=10)
        Label(self.result_frame,text = f"         Status   : {text}\nModel Used :  GBDT Svm\nAccuracy   :  88.70%",font = self.myfont,bg = '#2e2b2b',fg = 'white').place(x = 10,y = 300)

    def generate_result(self):
        self.input = self.preprocessing_review(self.input)
        print(self.input)
        df = pd.read_csv('C:\\Users\\vikra\\Desktop\\preprocessed_reviews.csv')
        tf_idf_vect = TfidfVectorizer(ngram_range=(1, 2), min_df=10)
        tf_idf_vect.fit(df['review'].values[:40000])
        final_tf_idf = tf_idf_vect.transform([self.input])
        filename = 'C:\\Users\\vikra\\Desktop\\finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.predict(final_tf_idf)
        return result
    def back(self):
        self.result_frame.destroy()
        self.__init__(self.master)

    def preprocessing_review(self,input):
        sentence = re.sub(r"http\S+", "",input)
        sentence = BeautifulSoup(sentence, 'lxml').get_text()
        sentence = self.decontracted(sentence)
        sentence = re.sub("\S*\d\S*", "", sentence).strip()
        sentence = re.sub('[^A-Za-z]+', ' ', sentence)
        ps = PorterStemmer()
        sentence = ' '.join([ps.stem(word) for word in sentence.split()])
        all_stopwords = stopwords.words('english')
        all_stopwords = set([all_stopwords.remove('not')])
        sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in all_stopwords)
        return sentence

    def decontracted(self,phrase):
        # specific
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        # genrel

        phrase = re.sub(r"n\'t'", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        return phrase
root = tkinter.Tk()
root.title("Application")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenwidth()))
root.resizable(False, False)
app = IMDB(root)
root.mainloop()