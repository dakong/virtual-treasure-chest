export async function fetchTreasureItems() {
    try {
        const result = await fetch('/api/treasureitem/', { method: 'GET' });
        return result.json();
    } catch(e) {
        console.log('Error occured: ', e);
    }
}

export async function purchaseItem(studentId, treasureItemId) {
    try {
        const result = await fetch('/api/purchase/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'student_id': studentId, 'treasure_item_id': treasureItemId})
        });
        return result.json();
    } catch (e) {
        console.log('Error occured: ', e);
    }
}