import { useState } from 'react'
import UploadForm from './components/UploadForm'
import ChatBox from './components/ChatBox'
import SummaryBox from './components/SummaryBox'
import TimestampBox from './components/TimestampBox'
import VideoPlayer from './components/VideoPlayer'

function App() {
    const [uploadedVideoUrl, setUploadedVideoUrl] = useState('')

    const summary = `
    This is AI generated summary.
    `

    const timestamps = [
        {
            topic:'Introduction',
            time:'00:30'
        },
        {
            topic:'Conclusion',
            time:'02:00'
        }
    ]

    return (
        <div className="container">

            <h1>
                AI Multimedia Q&A App
            </h1>

            <UploadForm
                onUploadSuccess={(data) => {
                    if (data.file_type === 'video') {
                        setUploadedVideoUrl(data.file_url)
                    }
                }}
            />

            <ChatBox />

            <SummaryBox
                summary={summary}
            />

            <TimestampBox
                timestamps={timestamps}
            />

            <VideoPlayer videoUrl={uploadedVideoUrl} />

        </div>
    )
}

export default App