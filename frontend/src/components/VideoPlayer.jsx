import { useRef } from 'react'

function VideoPlayer({ videoUrl, jumpToSeconds = null }) {

    const videoRef = useRef()

    const jumpToTime = (seconds) => {
        if (!videoRef.current) return

        videoRef.current.currentTime = seconds

        videoRef.current.play()
    }

    return (
        <div className="card">

            <h2>Video Player</h2>

            {
                videoUrl ? (
                    <video
                        ref={videoRef}
                        key={videoUrl}
                        width="100%"
                        controls
                        onLoadedMetadata={() => {
                            if (typeof jumpToSeconds === 'number') {
                                jumpToTime(jumpToSeconds)
                            }
                        }}
                    >
                        <source
                            src={videoUrl}
                            type="video/mp4"
                        />
                    </video>
                ) : (
                    <p>Upload a video file to preview it here.</p>
                )
            }

            <button onClick={()=>jumpToTime(30)} disabled={!videoUrl}>
                Play From 30s
            </button>

        </div>
    )
}

export default VideoPlayer