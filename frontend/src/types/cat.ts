export interface Cat {
    id: number;
    name: string;
    years_of_experience: number;
    breed: string;
    salary: number;
}

export interface CatCreate {
    name: string;
    years_of_experience: number;
    breed: string;
    salary: number;
}

export interface CatUpdate {
    salary: number;
}
