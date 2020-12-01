import { result } from 'lodash';
import debounce from 'lodash/debounce';

let updateStudentPoints = debounce(async function (data) {
    try {
        const result = await fetch('/api/student/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return result
    } catch (e) {
        console.log('Error occured:', e);
    }
}, 500);

export async function updateStudent(data) {
    try {
        const result = await updateStudentPoints(data, resolve, reject);
        return result;
    } catch(e) {
        console.log('Error occured: ', e);
    }
}