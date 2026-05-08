function TimestampBox({timestamps}) {

    return (
        <div className="card">

            <h2>Timestamps</h2>

            {
                timestamps.map((item,index)=>(
                    <div key={index}>

                        <p>
                            {item.topic} - {item.time}
                        </p>

                    </div>
                ))
            }

        </div>
    )
}

export default TimestampBox