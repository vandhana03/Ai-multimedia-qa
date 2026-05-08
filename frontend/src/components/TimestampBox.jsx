import { useState } from 'react'

function TimestampBox({ timestamps, onFindTimestamps, onJumpToTimestamp, loading }) {
    const [topic, setTopic] = useState('')
    const hasTimestamps = timestamps.length > 0

    const handleFind = () => {
        if (!topic.trim()) return
        onFindTimestamps(topic)
    }

    return (
        <div className="card">

            <h2>Timestamps</h2>
            <p className="muted-text">Find key moments by topic and jump directly in the video.</p>

            <div className="inline-group">
                <input
                    type="text"
                    placeholder="Enter topic (e.g. pricing)"
                    value={topic}
                    onChange={(e)=>setTopic(e.target.value)}
                />
                <button
                    onClick={handleFind}
                    disabled={loading || !topic.trim()}
                    className="compact-btn"
                >
                    {loading ? 'Finding...' : 'Find'}
                </button>
            </div>

            {
                hasTimestamps ? timestamps.map((item,index)=>(
                    <div key={index} className="timestamp-item">

                        <p className="timestamp-label">
                            <span>{item.topic}</span>
                            <strong>{item.time}</strong>
                        </p>
                        <button
                            onClick={()=>onJumpToTimestamp(item.seconds)}
                            className="compact-btn ghost-btn"
                        >
                            Play
                        </button>

                    </div>
                )) : <p className="muted-text">No timestamps yet.</p>
            }

        </div>
    )
}

export default TimestampBox