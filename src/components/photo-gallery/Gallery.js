import React, { useState, useLayoutEffect, useRef, Fragment, useEffect, Suspense } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { setPhotos, getPhotos} from '../../redux/gallery/photoSlice'
import PropTypes from 'prop-types';
import ResizeObserver from 'resize-observer-polyfill';
import { photoPropType } from './Photo';
// import { computeColumnLayout } from './layouts/columns';
// import { computeRowLayout } from './layouts/justified';
// import { findIdealNodeSearch } from './utils/findIdealNodeSearch';
// import LazyLoad from 'react-lazyload'
import moment from 'moment';
import PhotoLoading from './PhotoLoading';
import DateLabel from './DateLabel';
import Photo from './Photo';
import {GalleryBuilder} from './GalleryBuilder';
// const Photo = React.lazy(() => import("./Photo"));

const builder = new GalleryBuilder();
/**
 * https://javascript.plainenglish.io/react-infinite-scrolling-and-lazy-loading-171909f92b54
 */
const Gallery = React.memo(function Gallery({
  photos,
  onClick,
  direction,
  margin,
  limitNodeSearch,
  targetRowHeight,
  columns,
  renderImage
}) {
  const [containerWidth, setContainerWidth] = useState(0);
  
  // const [listItems, setListItems] = useState([]);
  const [isFetching, setIsFetching] = useState(false);
  const [page, setPage] = useState(1);
  
  const galleryEl = useRef(null);
  let renderComponent = renderImage || Photo;
  let dateLatest = moment();
  // let galleryStyle, thumbs = [];
  const photosData = useSelector(getPhotos)
  // const containerWidth = useSelector(getContainerWidth)
  const dispatch = useDispatch();
  builder.init({photos, direction, margin, limitNodeSearch, targetRowHeight, columns});

  const fetchData = async () => {
		// setTimeout(async () => {
			// const result = await fetch(`https://picsum.photos/v2/list?page=${page}`);
			// const data = await result.json();
      
      //console.trace();
      // const data = thumbs.slice(offset*(page-1), offset*page);
      const data = builder.getPaginate(page);
      if( data.length < 1){
        return;
      }
			setPage(page + 1);
      
      dispatch(setPhotos(data));

			// setListItems(() => {
			// 	return [...listItems, ...data];
			// });
    // }, 1000);
  }

  useLayoutEffect(() => {
    let animationFrameID = null;
    const observer = new ResizeObserver(entries => {
      // only do something if width changes
      const newWidth = entries[0].contentRect.width;
      if (containerWidth !== newWidth) {
        // put in an animation frame to stop "benign errors" from
        // ResizObserver https://stackoverflow.com/questions/49384120/resizeobserver-loop-limit-exceeded
        animationFrameID = window.requestAnimationFrame(() => {
          //setContainerWidth(Math.floor(newWidth));
        
        setContainerWidth( builder.setContainerWidth( newWidth ) );
        //containerWidth = builder.getContainerWidth();
          // dispatch(setContainerWidth(Math.floor(newWidth)));
        });
        // dispatch(setData({direction, limitNodeSearch, targetRowHeight, columns, margin, photos}));
        
      }
    });

    observer.observe(galleryEl.current);

    return () => {
      observer.disconnect();
      window.cancelAnimationFrame(animationFrameID);
    };

  });

  useEffect(()=>{
    fetchData();
    
    window.addEventListener('scroll', handleScroll);
  }, [containerWidth])

  useEffect(() => {
    if (!isFetching) return;
    fetchMoreListItems();
  }, [isFetching]);

  const handleClick = (event, { index }) => {
    onClick(event, {
      index,
      photo: photos[index],
      previous: photos[index - 1] || null,
      next: photos[index + 1] || null,
    });
  };

  // useEffect(() => {
	// 	fetchData();
	// 	window.addEventListener('scroll', handleScroll);
	// }, []);
  

  const handleScroll = () => {
		if (
			Math.ceil(window.innerHeight + document.documentElement.scrollTop) !== document.documentElement.offsetHeight ||
			isFetching
		)
			return;
		setIsFetching(true);
		console.log(isFetching);
	};

  const fetchMoreListItems = () => {
    fetchData();
    setIsFetching(false);
  };
  
  // no containerWidth until after first render with refs, skip calculations and render nothing
  if (!containerWidth) {
    return <div ref={galleryEl}>&nbsp;</div>;
  }
  
  //builder.setContainerWidth(containerWidth);

  const styles = builder.getStyle();
  
  return (
    <div className="react-photo-gallery--gallery">
      <div ref={galleryEl} style={styles}>
        {photosData.map((thumb, index) => {
          const { left, top, containerHeight, ...photo } = thumb;
          const date = moment(thumb.date);
          let showDate = false;
          if( !dateLatest.isSame(date, 'day')){
            showDate = true;
            dateLatest = date;
          }
         
          return <Fragment key={index} >
            {/* <PhotoLoading photo={photo} /> */}
            <Suspense fallback={<PhotoLoading photo={photo} />}>
  						{ showDate && <DateLabel date={dateLatest} /> }
              {/* <LazyLoad  placeholder={<PhotoLoading />} offset={20} > */}
                {renderComponent({
                  left,
                  top,
                  key: thumb.key || thumb.src,
                  containerHeight,
                  index,
                  margin,
                  direction,
                  onClick: onClick ? handleClick : null,
                  photo,
                })}
              {/* </LazyLoad> */}
					  </Suspense>
          </Fragment>;
        })}
        {isFetching && <h1>Fetching more list items...</h1>}

      </div>
    </div>
  );
});

Gallery.propTypes = {
  photos: PropTypes.arrayOf(photoPropType).isRequired,
  direction: PropTypes.string,
  onClick: PropTypes.func,
  columns: PropTypes.oneOfType([PropTypes.func, PropTypes.number]),
  targetRowHeight: PropTypes.oneOfType([PropTypes.func, PropTypes.number]),
  limitNodeSearch: PropTypes.oneOfType([PropTypes.func, PropTypes.number]),
  margin: PropTypes.number,
  renderImage: PropTypes.func,
};

Gallery.defaultProps = {
  margin: 2,
  direction: 'row',
  targetRowHeight: 300,
};
export { Photo };
export default Gallery;
