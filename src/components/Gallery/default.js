import React, { useState, useCallback } from "react";
import Carousel, { Modal, ModalGateway } from "react-images";
import { useSelector } from 'react-redux'
import { getPhotos } from '../../redux/gallery/photoSlice'
import { Gallery } from "../photo-gallery";
import { dnsRandom } from "../photo-gallery/utils/env";
import {images} from "./data";
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

    const photosViewalble = useSelector(getPhotos);
    return <>
    <Gallery photos={images} onClick={openLightbox} direction={"row"} />
     
     <ModalGateway>
       {viewerIsOpen ? (
         <Modal onClose={closeLightbox}>
           <Carousel
             currentIndex={currentImage}
             views={photosViewalble.map(x => ({
               ...x,
               caption: "x.title",
               alt:"alt",
               source: {
                 // fullscreen: x.src,
                 regular: `${dnsRandom(x.src)}`,
                 thumbnail: `${dnsRandom(x.thumbnail)}`
               }
             }))}
           />
         </Modal>
       ) : null}
     </ModalGateway>
    </>
}

export default GalleryDefault;