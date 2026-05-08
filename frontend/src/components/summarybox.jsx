function SummaryBox({ summary, onGenerateSummary, loading }) {

    return (
        <div className="card">

            <h2>Summary</h2>

            <button onClick={onGenerateSummary} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Summary'}
            </button>

            <p>{summary}</p>

        </div>
    )
}

export default SummaryBox