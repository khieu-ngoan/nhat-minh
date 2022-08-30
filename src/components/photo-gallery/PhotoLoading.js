import React from 'react';

const PhotoLoading = ({photo}) => {
    if( !photo ){
        return <></>;
    }
    console.log(`================`, {photo})
    const styles = {
        width: photo.width,
        heigth: photo.heigth,
    };
    return <>
    <div className="img-loading" style={styles}>
        <h5>Loading...</h5>
    </div>
    </>
};

export default PhotoLoading;
