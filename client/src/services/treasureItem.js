export async function fetchTreasureItems() {
    try {
        const result = await fetch('/api/treasureitem/', { method: 'GET' });
        return result.json();
    } catch(e) {
        console.log('Error occured: ', e);
    }
}
