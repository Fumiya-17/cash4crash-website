let carsData = [];

async function fetchCarsData() {
  try {
    const res = await fetch('/api/cars');
    if (res.ok) {
       const data = await res.json();
       carsData = data.map(c => ({
           id: c.id,
           brand: c.brand,
           name: c.name,
           make: c.make,
           model: c.model_year,
           image: c.image,
           price: c.price,
           specs: c.specs
       }));
    } else {
       console.error("Failed to fetch cars from database");
    }
  } catch (err) {
    console.error('Error fetching cars:', err);
  }
}
