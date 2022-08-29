import moment from 'moment';
import React from 'react';
import momentPropTypes from 'react-moment-proptypes';

const DateLabel = ({date}) => {
    if( !moment.isMoment(date) ){
        console.log(`==== date`, {date})
    }
    
    return <>
        <h5 className='gal-date-label'>{ moment.isMoment(date) ? date.format('MM/DD/YYYY') : "xome date show here"}</h5>
    </>
};
DateLabel.propTypes = {
    date: momentPropTypes.momentObj,
}

DateLabel.defaultProps = {
    date: moment(),
};
export default DateLabel;
