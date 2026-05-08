import { useState } from 'react'
import axios from 'axios'

function ChatBox() {

    const [question,setQuestion] = useState('')
    const [answer,setAnswer] = useState('')

    const askQuestion = async () => {

        try{

            const response = await axios.post(
                'http://127.0.0.1:8000/api/chat/',
                {
                    question:question
                }
            )

            setAnswer(response.data.answer)

        }catch(error){
            console.log(error)
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

            <button onClick={askQuestion}>
                Ask
            </button>

            {
                answer && (
                    <div>

                        <h3>Answer</h3>

                        <p>{answer}</p>

                    </div>
                )
            }

        </div>
    )
}

export default ChatBox