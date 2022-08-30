import React from 'react';
import PropTypes from 'prop-types';
import { IMAGE_URL } from './utils/env';

const imgWithClick = { cursor: 'pointer' };

const Photo = ({ index, onClick, photo, margin, direction, top, left, key }) => {
  const imgStyle = { margin: margin, display: 'block' };
  if (direction === 'column') {
    imgStyle.position = 'absolute';
    imgStyle.left = left;
    imgStyle.top = top;
  }

  const handleClick = event => {
    onClick(event, { photo, index });
  };

  
  photo.src = `${IMAGE_URL}/${photo.src}`;
  // photo.src = `${IMAGE_URL}/thumbnail/svg.svg`;
  // let imgPreload = `${IMAGE_URL}/${photo.thumbnail}`;

  return (
    // <LazyLoad key={key} once={true} placeholder={<img src={imgPreload} alt="..." />} >
     <img
      key={key}
      style={onClick ? { ...imgStyle, ...imgWithClick } : imgStyle}
      {...photo}
      onClick={onClick ? handleClick : null}
      alt={photo.src}
      title={photo.src}
    />
  // </LazyLoad>
  );
};

export const photoPropType = PropTypes.shape({
  key: PropTypes.string,
  src: PropTypes.string.isRequired,
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  alt: PropTypes.string,
  title: PropTypes.string,
  srcSet: PropTypes.oneOfType([PropTypes.string, PropTypes.array]),
  sizes: PropTypes.oneOfType([PropTypes.string, PropTypes.array]),
});

Photo.propTypes = {
  index: PropTypes.number.isRequired,
  onClick: PropTypes.func,
  photo: photoPropType.isRequired,
  margin: PropTypes.number,
  top: props => {
    if (props.direction === 'column' && typeof props.top !== 'number') {
      return new Error('top is a required number when direction is set to `column`');
    }
  },
  left: props => {
    if (props.direction === 'column' && typeof props.left !== 'number') {
      return new Error('left is a required number when direction is set to `column`');
    }
  },
  direction: PropTypes.string,
};

export default Photo;
