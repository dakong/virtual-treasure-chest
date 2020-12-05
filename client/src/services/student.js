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

export async function verifyStudent(data) {
    try {
        const result = await fetch('/verify/', {
            method: 'POST',
            headers: new Headers({
                "Authorization": `Basic ${btoa(`${data.userID}:${data.passcode}`)}`
            })
        });

        return result.json();
    } catch(e) {
        console.log('Error occured: ', e);
    }
}

export async function studentLogout() {
    try {
        const result = await fetch('/logoutstudent/', { method: 'POST' });
        return result.json();
    } catch(e) {
        console.log('Error occured: ', e);
    }
}