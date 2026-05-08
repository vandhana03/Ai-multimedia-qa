import { useState } from 'react'
import axios from 'axios'

function UploadForm({ onUploadSuccess }) {

    const [title,setTitle] = useState('')
    const [file,setFile] = useState(null)
    const [uploading, setUploading] = useState(false)

    const handleUpload = async () => {
        if (!title.trim()) {
            alert('Please enter a title')
            return
        }

        if (!file) {
            alert('Please choose a file')
            return
        }

        const formData = new FormData()

        formData.append('title',title)
        formData.append('file',file)

        try{
            setUploading(true)

            const response = await axios.post(
                'http://127.0.0.1:8000/api/upload/',
                formData
            )

            alert('Uploaded Successfully')
            if (onUploadSuccess) {
                onUploadSuccess(response.data)
            }

        }catch(error){
            console.log(error)
            const message = error?.response?.data?.error || 'Upload Failed'
            alert(message)
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="card">

            <h2>Upload File</h2>

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

            <button onClick={handleUpload} disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>

        </div>
    )
}

export default UploadForm