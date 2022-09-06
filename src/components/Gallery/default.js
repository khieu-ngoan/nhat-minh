import React, { useState, useCallback } from "react";
import Carousel, { Modal, ModalGateway } from "react-images";
import { useSelector, useDispatch } from 'react-redux'
import { getPhotos } from '../../redux/gallery/photoSlice'
import { Gallery, IMAGE_URL } from "../photo-gallery";
import images from '../../data.json';
import "./Gallery.css"
/**
 * react-photo-gallery 
 * http://neptunian.github.io/react-photo-gallery/api.html
 * @returns 
 */

function GalleryDefault() {
    const [currentImage, setCurrentImage] = useState(0);
    const [viewerIsOpen, setViewerIsOpen] = useState(false);

    const openLightbox = useCallback((event, { photo, index }) => {
        setCurrentImage(index);
        setViewerIsOpen(true);
    }, []);

    const closeLightbox = () => {
        setViewerIsOpen(false);
    };
    const photos = useSelector(getPhotos)

    return <>
    <Gallery photos={images} onClick={openLightbox} direction={"row"} />
     
     <ModalGateway>
       {viewerIsOpen ? (
         <Modal onClose={closeLightbox}>
           <Carousel
             currentIndex={currentImage}
             views={photos.map(x => ({
               ...x,
               caption: "x.title",
               alt:"alt",
               source: {
                 // download: x.src,
                 // fullscreen: x.src,
                 regular: `${IMAGE_URL}/${x.src}`,
                 thumbnail: `${IMAGE_URL}/${x.thumbnail}`
               }
             }))}
           />
         </Modal>
       ) : null}
     </ModalGateway>
    </>
}

export default GalleryDefault;