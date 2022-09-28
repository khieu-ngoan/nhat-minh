import { findIdealNodeSearch } from './utils/findIdealNodeSearch';
import { computeRowLayout } from './layouts/justified';
import { computeColumnLayout } from './layouts/columns';

const offset = 20;

// const galleryBuilder = (function() {
//     let instance;

//     function init() {
//       var number = 0;
//       return {
//         setNumber : function(x) {
//           number = x;
//         },
//         getNumber : function() {
//           return number;
//         }
//       };
//     }
  
//     return {
//       getInstance : function() {
//         if (!instance) instance = init();
//         return instance;
//       }
//     }
// })();

// export default galleryBuilder;

export class GalleryBuilder{
    constructor() {
        this.photos = [];
        this.direction = 'row';
        this.margin = 0;
        this.targetRowHeight = 0;
        // this.columns = columns;
        this.containerWidth = 0;
    }

    init(payload){
        if( this.photos.length > 0 ){
            return;
        }
        this.photos = payload.photos;
        this.direction = payload.direction;
        this.margin = payload.margin;
        this.limitNodeSearch = payload.limitNodeSearch;
        this.targetRowHeight = payload.targetRowHeight;
        this.columns = payload.columns;
        
    }

    setContainerWidth(width){
        this.containerWidth = Math.floor(width);
        this.setPhotos();
        return this.containerWidth;
    }

    getContainerWidth(){
        return this.containerWidth;
    }

    setPhotos(){
        // subtract 1 pixel because the browser may round up a pixel
        
        const { containerWidth } = this;
        const { margin, direction } = this;
        let { photos } = this;
        let { limitNodeSearch, targetRowHeight, columns } = this;
        let thumbs = [];
        const width = containerWidth - 1;

        if (this.direction === 'row') {
            // allow user to calculate limitNodeSearch from containerWidth
            if (typeof limitNodeSearch === 'function') {
                limitNodeSearch = limitNodeSearch(containerWidth);
            }
            if (typeof targetRowHeight === 'function') {
                targetRowHeight = targetRowHeight(containerWidth);
            }
            // set how many neighboring nodes the graph will visit
            if (limitNodeSearch === undefined) {
                limitNodeSearch = 2;
                if (containerWidth >= 450) {
                    limitNodeSearch = findIdealNodeSearch({ containerWidth, targetRowHeight });
                }
            }

            //galleryStyle = { display: 'flex', flexWrap: 'wrap', flexDirection: 'row' };
            thumbs = computeRowLayout({ containerWidth: width, limitNodeSearch, targetRowHeight, margin, photos });
        }

        if (direction === 'column') {
            // allow user to calculate columns from containerWidth
            if (typeof columns === 'function') {
            columns = columns(containerWidth);
            }
            // set default breakpoints if user doesn't specify columns prop
            if (columns === undefined) {
            columns = 1;
            if (containerWidth >= 500) columns = 2;
            if (containerWidth >= 900) columns = 3;
            if (containerWidth >= 1500) columns = 4;
            }
            //galleryStyle = { position: 'relative' };
            thumbs = computeColumnLayout({ containerWidth: width, columns, margin, photos });
            //galleryStyle.height = thumbs[thumbs.length - 1].containerHeight;
        }

        this.photos = thumbs;
    }

    getPaginate(page){
        // const { containerWidth, photos } = this;
        if( this.containerWidth < 1 ){
            return [];
        }
        const data = this.photos.slice(offset*(page-1), offset*page);
        return data;
    }

    getStyle(){
        // const width = containerWidth - 1;
        const { containerWidth } = this;
        const { direction } = this;
        let { columns } = this;
        // let {limitNodeSearch, targetRowHeight} = this;
        // let thumbs = [];
        let style = {};

        if (this.direction === 'row') {
            // allow user to calculate limitNodeSearch from containerWidth
            // if (typeof limitNodeSearch === 'function') {
            // limitNodeSearch = limitNodeSearch(containerWidth);
            // }
            // if (typeof targetRowHeight === 'function') {
            // targetRowHeight = targetRowHeight(containerWidth);
            // }
            // // set how many neighboring nodes the graph will visit
            // if (limitNodeSearch === undefined) {
            // limitNodeSearch = 2;
            // if (containerWidth >= 450) {
            //     limitNodeSearch = findIdealNodeSearch({ containerWidth, targetRowHeight });
            // }
            // }

            style = { display: 'flex', flexWrap: 'wrap', flexDirection: 'row' };
            //thumbs = computeRowLayout({ containerWidth: width, limitNodeSearch, targetRowHeight, margin, photos });
        }
        if (direction === 'column') {
            // allow user to calculate columns from containerWidth
            if (typeof columns === 'function') {
            columns = columns(containerWidth);
            }
            // set default breakpoints if user doesn't specify columns prop
            if (columns === undefined) {
            columns = 1;
            if (containerWidth >= 500) columns = 2;
            if (containerWidth >= 900) columns = 3;
            if (containerWidth >= 1500) columns = 4;
            }
            style = { position: 'relative' };
            //thumbs = computeColumnLayout({ containerWidth: width, columns, margin, photos });
            //galleryStyle.height = thumbs[thumbs.length - 1].containerHeight;
        }

        return style;
    }

}