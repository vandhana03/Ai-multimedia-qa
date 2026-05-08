import { forwardRef } from 'react'

// ref is forwarded directly to the <video> element
// App.jsx can then call: videoRef.current.currentTime = x; videoRef.current.play()
const VideoPlayer = forwardRef(function VideoPlayer({ videoUrl }, ref) {
    return (
        <div className="card">
            <h2>Video Player</h2>
            <p className="muted-text">Use timestamps to jump to relevant moments instantly.</p>

            {videoUrl ? (
                <video
                    className="video-frame"
                    ref={ref}
                    key={videoUrl}
                    width="100%"
                    controls
                >
                    <source src={videoUrl} type="video/mp4" />
                </video>
            ) : (
                <p className="muted-text">Upload a video file to preview it here.</p>
            )}
        </div>
    )
})

export default VideoPlayer