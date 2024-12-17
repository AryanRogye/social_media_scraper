import React, { ChangeEventHandler, useState } from 'react';
import "./App.css";

function App() {
    const [selectedFile, setSelectedFile] = useState<String>("")
    const manageSelectedFile = (file : React.ChangeEvent<HTMLInputElement>) => {
        if (file.target.files != null) {
            let filename = file.target.files[0].name.toString()
            if (!(filename.endsWith(".db") || filename.endsWith(".txt") || filename.endsWith(".json"))) {
                setSelectedFile(file.target.files[0].name)
            } else {
                console.log("Wrong Format")
            }
        }
    } 
    return (
        <div className='container'>
            <h1>Welcome Select File Here</h1>
            <div>
                <input type='file' accept='.db,.txt,.json,text/plain,application/json' onChange={manageSelectedFile}/>
            </div>
            <div>
                {selectedFile !== "" && <p>Selected File: {selectedFile.toString()}</p>}
            </div>
        </div>
    );
}

export default App;
