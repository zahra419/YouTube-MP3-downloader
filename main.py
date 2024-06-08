from flask import Flask, render_template, request,redirect, url_for
from pytube import YouTube
import math , os 
import pytube.exceptions

app=Flask(__name__, template_folder='templates')



@app.route("/", methods=["GET"])
def index():
    video=request.args.get('ytvideo','')
    if video != "" :
      try:
        yt=YouTube(video)
      except pytube.exceptions.PytubeError as e:
        return redirect(url_for('error'))
      else:
        title=yt.title
        thumbnail_url=yt.thumbnail_url
        totalseconds=yt.length
        author=yt.author
        hr=math.floor(totalseconds/3600)
        totalseconds%=3600
        min=math.floor(totalseconds/60)
        sec=totalseconds%60
        length=str(hr).zfill(2)+':'+str(min).zfill(2)+':'+str(sec).zfill(2)
        audio_file = yt.streams.filter(only_audio=True).first()
        path='.'
        file=audio_file.download(output_path=path)
        base,ext=os.path.splitext(file)
        new_file=base+'.mp3'
        os.rename(file,new_file)
        return render_template('index.html',show=True,title=title,thumbnail=thumbnail_url,length=length, author=author)
    else:
       return render_template('index.html',show=False)

@app.route('/error')
def error():
  return render_template('error.html',message='There s error , try again!')



  

   
   
if __name__ == "__main__":
    app.run(debug=False,port=8080)