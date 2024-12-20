import { useState } from 'react';
import "./App.css";
import { invoke } from '@tauri-apps/api/core';
import toast from 'react-hot-toast';

function App() {
    const [selectedFile, setSelectedFile] = useState< String | undefined >("")
    const [fullFilePath, setFullFilePath] = useState< String | undefined >("")

    const limit : number = 10
    // Should be an array of Instagram Accounts
    const [InstagramAccount, setInstagramAccount] = useState<String[]>([]);
    const [fullPathInstagramAccount, setFullPathInstagramAccount] = useState<any>();
    
    const openWindows = async () => {
        if (!fullPathInstagramAccount || fullPathInstagramAccount.length === 0) {
            toast.error("No data available to send");
            return;
        }
        try {
            // Send the JSON data to the backend
            const response: String = await invoke("open_sel", {
                jsonData: JSON.stringify(fullPathInstagramAccount), // Serialize the data
                file: fullFilePath,
            });
            if (response) {
                toast.success("Success: Data sent to backend!");
                console.log("Backend Response:", response);
            }
        } catch (error: any) {
            console.error("Error Sending Data:", error);
            toast.error("Something Went Wrong", error);
        }
    };

    const parseFile = async() => {
        if (!fullFilePath) {
            toast.error("File Path Not Set")
        }
        try {
            // Convert the string to a integer
            // First Check if instance is a String
            let response : string = await invoke("parse_file", {file: fullFilePath, limit: limit})
            if (response) {
                const users = JSON.parse(response);
                setFullPathInstagramAccount(users)
                
                let accounts = users
                    .map((user: {"Instagram Account" : string}) => user["Instagram Account"])
                    .join(", ")

                // Split by comma and clean up the usernames
                const splitAccounts = accounts.split(", ").map((link: string) =>
                    link.replace("https://www.instagram.com/", "").replace("/", "")
                );

                // Store the cleaned usernames in `InstagramAccount`
                setInstagramAccount(splitAccounts);

                console.log("Full Paths:", accounts);
                console.log("Usernames:", splitAccounts);

                setInstagramAccount(splitAccounts)
            }
        } catch (error: any) {
            toast.error("Error Parsing File\n" + error.message)
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
        } catch (error : any) {
            toast.error("Problem Getting File\n" + error.message)
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
                        <p className='button-text'>Parse File</p>
                    </button>
                    <button className='parse-file-button' onClick={() => {
                        openWindows();
                    }}>
                        <p className='button-text'>Open Messages</p>
                    </button>
                </div>
                <div className='users-box'>
                    {fullPathInstagramAccount && <p>Users</p>}
                    <ul className='user-list'>
                        {InstagramAccount.map((account, index) => (
                            <li key={index}>{account}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default App;
