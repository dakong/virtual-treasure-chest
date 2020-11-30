import debounce from 'lodash/debounce';

let updateStudentPoints = debounce((data, resolve) => {
    fetch('/api/student/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(result => resolve(result)), 500;
}, 500);

export function updateStudent(data) {
    return new Promise((resolve, reject) => {
        updateStudentPoints(data, resolve, reject)
    });
}