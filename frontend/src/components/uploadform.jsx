import { useState } from 'react'
import axios from 'axios'

function UploadForm({ onUploadSuccess }) {

    const [title,setTitle] = useState('')
    const [file,setFile] = useState(null)
    const [uploading, setUploading] = useState(false)
    const [message, setMessage] = useState('')
    const [messageType, setMessageType] = useState('')

    const handleUpload = async () => {
        if (!title.trim()) {
            setMessage('Please enter a title.')
            setMessageType('error')
            return
        }

        if (!file) {
            setMessage('Please choose a file.')
            setMessageType('error')
            return
        }

        const formData = new FormData()

        formData.append('title',title)
        formData.append('file',file)

        try{
            setUploading(true)
            setMessage('')

            const response = await axios.post(
                'http://127.0.0.1:8000/api/upload/',
                formData
            )

            setMessage('Upload completed successfully.')
            setMessageType('success')
            if (onUploadSuccess) {
                onUploadSuccess(response.data)
            }

        }catch(error){
            console.log(error)
            const message = error?.response?.data?.error || 'Upload Failed'
            setMessage(message)
            setMessageType('error')
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="card">

            <h2>Upload File</h2>
            <p className="muted-text">Supported formats: PDF, MP3, WAV, M4A, MP4, MOV, WEBM, MKV.</p>

            <input
                type="text"
                placeholder="Enter title"
                value={title}
                onChange={(e)=>setTitle(e.target.value)}
            />

            <input
                type="file"
                accept=".pdf,.mp3,.wav,.m4a,.mp4,.mov,.webm,.mkv"
                onChange={(e)=>setFile(e.target.files[0])}
            />

            {file ? <p className="muted-text">Selected: {file.name}</p> : null}

            <button onClick={handleUpload} disabled={uploading || !title.trim() || !file}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>
            {message ? <p className={`status-text ${messageType}`}>{message}</p> : null}

        </div>
    )
}

export default UploadForm