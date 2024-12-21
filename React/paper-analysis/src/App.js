import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import './App.css';
import Stack from '@mui/material/Stack';
import React, { useState } from "react";
import Context from './Context';
import CircularProgress from '@mui/material/CircularProgress';

function App() {
  const [searchValue, setSearchValue] = useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleInputChange = (event) =>{
    setSearchValue(event.target.value);
  }

  const handleSubmit = async () =>{
    setLoading(true);
    try{
      const res = await fetch(`http://localhost:8585/api/news/process?category=${searchValue}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"}
      })
      if (res.ok){
        const data = await res.json()
        console.log(data)
        setSearchValue(data)
        setLoading(false)
      }
      else{
        console.log("Error: ", res.status, res.statusText)
        setLoading(false)
      }
    }
    catch(error){
      console.log(error)
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <Box
        sx={{ width: 500, maxWidth: '100%' }}

      >
          <TextField sx={{width: 500}} id="outlined-basic" label="news" onChange={handleInputChange} />
      </Box>
      
      <Stack direction="row" spacing={1}>
          <IconButton color="primary" aria-label="search" onClick={handleSubmit}>
            <SearchIcon />
       </IconButton>
    </Stack>
      </header>
      {loading && (
        <div className='loader-overlay'>
          <CircularProgress />
        </div>
      )}
      
        <Context data={searchValue}></Context>
    </div>
  );
}

export default App;
