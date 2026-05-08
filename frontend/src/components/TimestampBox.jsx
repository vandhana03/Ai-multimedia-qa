import { useState } from 'react'

function TimestampBox({ timestamps, onFindTimestamps, onJumpToTimestamp, loading }) {
    const [topic, setTopic] = useState('')

    return (
        <div className="card">

            <h2>Timestamps</h2>

            <div style={{display:'flex', gap:'8px', marginBottom:'10px'}}>
                <input
                    type="text"
                    placeholder="Enter topic (e.g. pricing)"
                    value={topic}
                    onChange={(e)=>setTopic(e.target.value)}
                />
                <button
                    onClick={()=>onFindTimestamps(topic)}
                    disabled={loading}
                >
                    {loading ? 'Finding...' : 'Find'}
                </button>
            </div>

            {
                timestamps.length > 0 ? timestamps.map((item,index)=>(
                    <div key={index}>

                        <p>
                            {item.topic} - {item.time}
                        </p>
                        <button
                            onClick={()=>onJumpToTimestamp(item.seconds)}
                        >
                            Play
                        </button>

                    </div>
                )) : <p>No timestamps yet.</p>
            }

        </div>
    )
}

export default TimestampBox