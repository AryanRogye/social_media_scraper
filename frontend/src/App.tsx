import React, { ChangeEventHandler, useState } from 'react';
import "./App.css";
import { invoke } from '@tauri-apps/api/core';
import toast from 'react-hot-toast';

function App() {
    const [selectedFile, setSelectedFile] = useState< String | undefined >("")
    const [fullFilePath, setFullFilePath] = useState< String | undefined >("")

    const parseFile = async() => {
        try {
            await invoke("parse_file", {file: fullFilePath})
        } catch (error) {

        }
    }
    const handleClicked = async () => {
        try {
            const response : String = await invoke("open_finder", { name: "React Native"})
            // Format Just the last /____ whatever it may be
            const formatted_response = response.trim().split("/")
            if (response === "None") {
                toast.error("Try Again")
                return
            }
            setFullFilePath(response)
            setSelectedFile(formatted_response[formatted_response.length-1])
        } catch (error) {

        }
    }

    return (
        <div className='container'>
            <div>
                <h1 className=''>Welcome</h1>
                <div>
                    <div>
                        <h1>Select File</h1>
                    </div>
                    <div>
                        <button className="open-file-button" onClick={() => {
                            handleClicked()
                        }}>
                            <p>Open File</p>
                        </button>
                    </div>
                </div>
                <div>
                    {selectedFile !== "" && selectedFile && <p>Selected File: {selectedFile.toString()}</p>}
                </div>
                <div className='button-box'>
                    <button className='parse-file-button' onClick={() => {
                        parseFile();
                    }}>
                        <p className='button-text'>Parse File?</p>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;
