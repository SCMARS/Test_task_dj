const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getCats() {
    const res = await fetch(`${API_URL}/cats/`);
    if (!res.ok) throw new Error('Failed to fetch cats');
    return res.json();
}

export async function createCat(data: any) {
    const res = await fetch(`${API_URL}/cats/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Failed to create cat');
    }
    return res.json();
}

export async function deleteCat(id: number) {
    const res = await fetch(`${API_URL}/cats/${id}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete cat');
}

export async function updateCatSalary(id: number, salary: number) {
    const res = await fetch(`${API_URL}/cats/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ salary }),
    });
    if (!res.ok) throw new Error('Failed to update salary');
    return res.json();
}
