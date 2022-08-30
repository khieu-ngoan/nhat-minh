import React from "react";
import { useStyles } from "../components/material/style";
import { AppBar, Toolbar, Typography, Button, IconButton } from "../components/material/core";
import { MenuIcon } from "../components/material/icons";
import { GalleryDefault } from "../components/Gallery";
function App() {

  const classes = useStyles();
  
  return (
    <div>
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              Nhật Minh
            </Typography>
            <Button color="inherit">Login</Button>
          </Toolbar>
        </AppBar>
      </div>

      <GalleryDefault />
      
    </div>
  );
}

export default App;