import React, { useState, useEffect } from "react";
import "./App.css";

const TextModifier = () => {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [mapping, setMapping] = useState({});
  const [inputCharCount, setInputCharCount] = useState(0);
  const [outputCharCount, setOutputCharCount] = useState(0);
  const [inputTokenCount, setInputTokenCount] = useState(0);
  const [outputTokenCount, setOutputTokenCount] = useState(0);

  useEffect(() => {
    fetchCharAndTokenCount(inputText, setInputCharCount, setInputTokenCount);
    fetchCharAndTokenCount(outputText, setOutputCharCount, setOutputTokenCount);
  }, [inputText, outputText]);

  const fetchCharAndTokenCount = async (text, setCharCount, setTokenCount) => {
    const response = await fetch("http://localhost:5000/getCharAndTokenCount", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (response.ok) {
      const data = await response.json();
      setCharCount(data.charCount);
      setTokenCount(data.tokenCount);
    } else {
      console.error(
        "Failed to fetch character and token count:",
        response.status
      );
    }
  };

  const anonymize = async () => {
    const response = await fetch("http://localhost:5000/anonymize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText }),
    });

    if (response.ok) {
      const data = await response.json();
      setOutputText(data.anonymizedText);
      setMapping(data.mapping);
    } else {
      console.error("Failed to anonymize the text:", response.status);
    }
  };

  const decode = async () => {
    const response = await fetch("http://localhost:5000/decode", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: outputText, mapping: mapping }),
    });

    if (response.ok) {
      const data = await response.json();
      setOutputText(data.decodedText);
    } else {
      console.error("Failed to decode the text:", response.status);
    }
  };

  const removeSpacesAndLineBreaks = async () => {
    const response = await fetch(
      "http://localhost:5000/removeSpacesAndLineBreaks",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      }
    );

    if (response.ok) {
      const data = await response.json();
      setOutputText(data.text);
    } else {
      console.error("Failed to transform the text:", response.status);
    }
  };

  return (
    <div className="container">
      <div className="textareaContainer">
        <div className="inputContainer">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            className="inputArea"
          />
          <div className="countContainer">
            <div className="count">Character count: {inputCharCount}</div>
            <div className="count">Token count: {inputTokenCount}</div>
          </div>
        </div>
        <div className="buttonContainer">
          <button onClick={anonymize} className="anonymizeButton">
            Anonymize
          </button>
          <button
            onClick={removeSpacesAndLineBreaks}
            className="transformButton"
          >
            Remove Spaces
          </button>
        </div>
        <div className="outputContainer">
          <textarea
            value={outputText}
            onChange={(e) => setOutputText(e.target.value)}
            className="outputArea"
          />
          <div className="countContainer">
            <div className="count">Character count: {outputCharCount}</div>
            <div className="count">Token count: {outputTokenCount}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextModifier;
