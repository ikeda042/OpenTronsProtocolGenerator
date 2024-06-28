import React, { useState, useRef } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { Container, Stack, TextField } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import UploadFileIcon from '@mui/icons-material/UploadFile';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [downloadable, setDownloadable] = useState(false);
  const [cellValues, setCellValues] = useState<{ [key: string]: string }>({});
  const [protocolDownloadable, setProtocolDownloadable] = useState(false);
  const hiddenFileInput = useRef<HTMLInputElement>(null);
  const [protocolReady, setProtocolReady] = useState(false);


  const rowLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
      setDownloadable(true);
    }
  };

  const handleClick = () => {
    hiddenFileInput.current?.click();
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, key: string) => {
    setCellValues(prev => ({
      ...prev,
      [key]: event.target.value,
    }));
  };

  const downloadTemplate = async () => {
    try {
      const response = await fetch('http://localhost:8000/xlsx_template');
      if (!response.ok) throw new Error('Response not OK');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'template.xlsx');
      document.body.appendChild(link);
      link.click();
      link?.parentNode?.removeChild(link);
    } catch (error) {
      console.error('Download template error:', error);
    }
  };

  const downloadFile = async () => {
    try {
      const response = await fetch('http://localhost:8000/return-template/');
      if (!response.ok) throw new Error('Response not OK');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'return_template.py');
      document.body.appendChild(link);
      link.click();
      link?.parentNode?.removeChild(link);
    } catch (error) {
      console.error('Download error:', error);
    }
  };
  const handleSubmit = async () => {
    const valuesArray = [];
    for (let colIndex = 1; colIndex <= 12; colIndex++) {
      for (const rowLabel of rowLabels) {
        const key = `${rowLabel}-${colIndex}`;
        valuesArray.push(cellValues[key] || '');
      }
    }
    try {
      const response = await fetch('http://localhost:8000/submit-values/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ values: valuesArray }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      setProtocolReady(true);
    } catch (error) {
      console.error('Submit error:', error);
    }
  };


  return (
    <div>
      <AppBar position="static" sx={{ backgroundColor: '#000' }}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h5" component="div">
            OpenTrons Protocol Generator
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <div style={{ width: '100%', display: 'grid', gridTemplateColumns: 'repeat(13, 1fr)', gap: '1px', backgroundColor: '#ccc', marginBottom: '20px' }}>
          <div style={{ backgroundColor: '#fff', padding: '8px', textAlign: 'center' }}>
          </div>
          {Array.from({ length: 12 }).map((_, colIndex) => (
            <div
              key={`colLabel-${colIndex + 1}`}
              style={{
                backgroundColor: '#fff',
                padding: '8px',
                textAlign: 'center',
                border: '1px solid #ccc'
              }}
            >
              {colIndex + 1}
            </div>
          ))}
          {rowLabels.map((rowLabel, rowIndex) => (
            <React.Fragment key={`row-${rowLabel}`}>
              <div
                style={{
                  backgroundColor: '#fff',
                  padding: '8px',
                  textAlign: 'center',
                  border: '1px solid #ccc'
                }}
              >
                {rowLabel}
              </div>
              {Array.from({ length: 12 }).map((_, colIndex) => {
                const key = `${rowLabel}-${colIndex + 1}`;
                return (
                  <div
                    key={key}
                    style={{
                      backgroundColor: '#fff',
                      padding: '8px',
                      textAlign: 'center',
                      border: '1px solid #ccc'
                    }}
                  >
                    <TextField
                      variant="outlined"
                      size="small"
                      value={cellValues[key] || ''}
                      onChange={(e) => handleChange(e, key)}
                      autoComplete="off"
                    />
                  </div>
                );
              })}
            </React.Fragment>
          ))}
        </div>
        <input
          accept=".xlsx"
          type="file"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          ref={hiddenFileInput}
        />
        <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
          {/* <Button
            variant="contained"
            onClick={handleClick}
            sx={{ backgroundColor: '#000', color: '#fff' }}
            startIcon={<UploadFileIcon />}
          >
            xlsxファイルをアップロード
          </Button> */}
          <Button
            variant="contained"
            onClick={handleSubmit}
            startIcon={<UploadFileIcon />}
            sx={{ backgroundColor: '#000', color: '#fff' }}
          >
            プレートデータを送信
          </Button>
          <Button
            variant="contained"
            disabled={!protocolReady}
            onClick={downloadFile}
            startIcon={<DownloadIcon />}
            sx={{ backgroundColor: '#000', color: '#fff' }}
          >
            プロトコルをダウンロード(python)
          </Button>
          {/* <Button
            variant="contained"
            onClick={downloadTemplate}
            color='success'
            startIcon={<DownloadIcon />}
          >
            xlsxテンプレートをダウンロード
          </Button> */}
        </Stack>
      </Container>
    </div>
  );
}

export default App;
