import { useState } from 'react'
import axios from 'axios'
import UploadForm from './components/uploadform'
import ChatBox from './components/chatbox'
import SummaryBox from './components/summarybox'
import TimestampBox from './components/TimestampBox'
import VideoPlayer from './components/VideoPlayer'

function App() {
    const [uploadedVideoUrl, setUploadedVideoUrl] = useState('')
    const [summary, setSummary] = useState('Click "Generate Summary" after upload.')
    const [timestamps, setTimestamps] = useState([])
    const [summaryLoading, setSummaryLoading] = useState(false)
    const [timestampLoading, setTimestampLoading] = useState(false)
    const [jumpToSeconds, setJumpToSeconds] = useState(null)

    const handleGenerateSummary = async () => {
        try {
            setSummaryLoading(true)
            const response = await axios.post('http://127.0.0.1:8000/api/summary/')
            setSummary(response.data.summary || 'No summary generated.')
        } catch (error) {
            const message = error?.response?.data?.error || 'Failed to generate summary.'
            setSummary(message)
        } finally {
            setSummaryLoading(false)
        }
    }

    const handleFindTimestamps = async (topic) => {
        if (!topic?.trim()) return
        try {
            setTimestampLoading(true)
            const response = await axios.post(
                'http://127.0.0.1:8000/api/timestamps/',
                { topic }
            )
            setTimestamps(response.data.timestamps || [])
        } catch (error) {
            console.log(error)
            setTimestamps([])
        } finally {
            setTimestampLoading(false)
        }
    }

    return (
        <div className="container">

            <h1>
                AI Multimedia Q&A App
            </h1>

            <UploadForm
                onUploadSuccess={(data) => {
                    setSummary('Click "Generate Summary" after upload.')
                    setTimestamps([])
                    setJumpToSeconds(null)
                    if (data.file_type === 'video') {
                        setUploadedVideoUrl(data.file_url)
                    }
                }}
            />

            <ChatBox />

            <SummaryBox
                summary={summary}
                loading={summaryLoading}
                onGenerateSummary={handleGenerateSummary}
            />

            <TimestampBox
                timestamps={timestamps}
                loading={timestampLoading}
                onFindTimestamps={handleFindTimestamps}
                onJumpToTimestamp={(seconds) => setJumpToSeconds(seconds)}
            />

            <VideoPlayer
                videoUrl={uploadedVideoUrl}
                jumpToSeconds={jumpToSeconds}
            />

        </div>
    )
}

export default App