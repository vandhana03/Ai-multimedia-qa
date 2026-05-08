import { useState } from 'react'
import axios from 'axios'

function ChatBox() {

    const [question,setQuestion] = useState('')
    const [answer,setAnswer] = useState('')
    const [loading, setLoading] = useState(false)
    const [source, setSource] = useState('')

    const askQuestion = async () => {
        if (!question.trim()) return

        try{
            setLoading(true)

            const response = await axios.post(
                'http://127.0.0.1:8000/api/chat/',
                {
                    question:question
                }
            )

            setAnswer(response.data.answer)
            setSource(response.data.source_title || '')

        }catch(error){
            console.log(error)
            const message = error?.response?.data?.error || 'Failed to get answer'
            setAnswer(message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="card">

            <h2>AI Chatbot</h2>

            <textarea
                rows="4"
                placeholder="Ask question..."
                value={question}
                onChange={(e)=>setQuestion(e.target.value)}
            />

            <button onClick={askQuestion} disabled={loading}>
                {loading ? 'Asking...' : 'Ask'}
            </button>

            {
                answer && (
                    <div>

                        <h3>Answer</h3>

                        <p>{answer}</p>
                        {source ? <p><b>Source:</b> {source}</p> : null}

                    </div>
                )
            }

        </div>
    )
}

export default ChatBox