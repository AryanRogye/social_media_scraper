import React, { ChangeEventHandler, useState } from 'react';
import "./App.css";
import { invoke } from '@tauri-apps/api/core';

function App() {
    const [selectedFile, setSelectedFile] = useState<String | undefined >("")

    const handleClicked = async () => {
        try {
            const response : String = await invoke("open_finder", { name: "React Native"})
            // Format Just the last /____ whatever it may be
            const formatted_response = response.trim().split("/")
            setSelectedFile(formatted_response[formatted_response.length-1])
        } catch (error) {

        }
    }

    return (
        <div className='container'>
            <h1 className=''>Welcome</h1>
            <div>
                <h1>Select File</h1>
                <button className="logo" onClick={() => {
                    console.log("Handle Clicked")
                    handleClicked()
                }}>
                    <p>Open File</p>
                </button>
            </div>
            <div>
                {selectedFile !== "" && selectedFile && <p>Selected File: {selectedFile.toString()}</p>}
            </div>
        </div>
    );
}

export default App;
