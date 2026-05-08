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
            <p className="muted-text">Use timestamps to jump to relevant moments instantly.</p>

            {
                videoUrl ? (
                    <video
                        className="video-frame"
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
                    <p className="muted-text">Upload a video file to preview it here.</p>
                )
            }

        </div>
    )
}

export default VideoPlayer