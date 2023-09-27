

function postRecording(audio_video, audio_only, video_only){
    return new Promise((resolve, reject) => {
        setTimeout(() => {
          
          if (shouldError) {
            reject(new Error('Good guess but a wrong answer. Try again!'));
          } else {
            resolve();
          }
        }, 1500);
    })
}