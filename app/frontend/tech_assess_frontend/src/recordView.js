import { useReactMediaRecorder } from "react-media-recorder";


function RecordView(props){
  const { status, startRecording, stopRecording, mediaBlobUrl, onStop} =
    useReactMediaRecorder({ video: props.useVideo , audio: props.useAudio, onStop: props.onStop });
  return (
    <div>
      <p>{status}</p>
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
      <video src={mediaBlobUrl} controls autoPlay loop />
    </div>
  );
}


export default RecordView;