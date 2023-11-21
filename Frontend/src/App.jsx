import { useState } from 'react'
import './App.css'

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [threshold, setThreshold] = useState(0.5)
  const [file, setFile] = useState(null)
  const [processedImage, setProcessedImage] = useState(null)
  const [processedData, setProcessedData] = useState(null)
  const [selectedObjects, setSelectedObjects] = useState([])

  const [removedObjImg, setRemovedObjImg] = useState(null)

  const handleFileSelected = (e) => {
    const files = Array.from(e.target.files)
    setFile(files[0])
  }


  const handleUpload = async () => {
    setIsLoading(true)
    setProcessedImage(null)
    setProcessedData(null)
    setRemovedObjImg(null)
    setSelectedObjects([])
    const formData = new FormData()
    formData.append('image_file', file)

    const dataImage = await fetch(`http://127.0.0.1:3000/predict-image?confidence_threshold=${threshold}`, {
      method: 'POST',
      body: formData
    });

    const imageFile = await dataImage.blob()
    setProcessedImage(imageFile)


    const data = await fetch(`http://127.0.0.1:3000/predict-data?confidence_threshold=${threshold}`, {
      method: 'POST',
      body: formData
    });

    const dataJson = await data.json()
    setProcessedData(dataJson)
    console.log(dataJson)
    setIsLoading(false)
  }


  const handleUploadRemovedObj = async () => {
    setIsLoading(true)
    setRemovedObjImg(null)
    const formData = new FormData()
    formData.append('image_file', file)
    formData.append('confidence_threshold', threshold)
    const filtered  = processedData.filter((data) => selectedObjects.includes(data.class_name + data.instance_id))
    console.log(filtered)
    formData.append('items', JSON.stringify(filtered))

    const dataImage = await fetch('http://127.0.0.1:3000/remove-items-image', {
      method: 'POST',
      body: formData
    });

    const imageFile = await dataImage.blob()
    setRemovedObjImg(imageFile)
    setIsLoading(false)
  }

  const setSelectButton = (data) => {
    // () => setSelectedButtons([...selectedButtons, data.class_name + data.instance_id])
    if (selectedObjects.includes(data.class_name + data.instance_id)) {
      setSelectedObjects(selectedObjects.filter((item) => item !== data.class_name + data.instance_id))
    } else {
      setSelectedObjects([...selectedObjects, data.class_name + data.instance_id])
    }
  }


  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

      <div className="image-loader" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '10px' }}>
        <input type="file" onChange={handleFileSelected} />
        {file && (
          <>
            <img src={URL.createObjectURL(file)} alt="preview" />
            <button onClick={handleUpload}  disabled={isLoading} style={{ backgroundColor: 'red', color: 'white', margin: '10px' }}>Process</button>
          </>
        )}

      </div>

      <div className="image-processed" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {processedData && processedImage &&
          <>
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
              {processedImage && (
                <img src={URL.createObjectURL(processedImage)} alt="preview" />
              )}

              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '10px' }}>
                <h4>Select the objects that you want to remove</h4>
                {processedData?.map((data) => (
                  <button onClick={() => setSelectButton(data)}
                    style={{
                      backgroundColor: selectedObjects.includes(data.class_name + data.instance_id) ? 'red' : 'white',
                      color: selectedObjects.includes(data.class_name + " " + data.instance_id) ? 'white' : 'black',
                      margin: '10px'
                    }}
                  >Objet: {data.class_name + " " + data.instance_id}</button>
                ))}
              </div>
            </div>
            <button onClick={handleUploadRemovedObj} disabled={selectedObjects.length === 0 || isLoading}
            style={{ backgroundColor: 'red', color: 'white', margin: '10px' }}>Remove objects</button>
          </>}
      </div>

      <div className="image-without-objects" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {removedObjImg && <img src={URL.createObjectURL(removedObjImg)} alt="preview" />}
      </div>
    </div>
  )
}

export default App
