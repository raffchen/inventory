import { useForm } from "@refinedev/core";

export const LensCreate = () => {
  const { onFinish, mutation } = useForm();

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Using FormData to get the form values and convert it to an object.
    const data = Object.fromEntries(new FormData(event.currentTarget).entries());
    // Calling onFinish to submit with the data we've collected from the form.
    onFinish({
      ...data,
      sphere: Number(data.sphere),
      cylinder: Number(data.cylinder),
      unit_price: Number(data.unit_price).toFixed(2),
      quantity: data.quantity === "" ? 0 : Number(data.quantity),
      storage_limit: data.storage_limit === "" ? null : Number(data.storage_limit),
    });
  };

  return (
    <form onSubmit={onSubmit}>
      <label htmlFor="id">Id</label>
      <input type="text" id="id" name="id" required />

      <label htmlFor="lens_type">Lens Type</label>
      <input type="text" id="lens_type" name="lens_type" required />

      <label htmlFor="sphere">Sphere</label>
      <input type="number" id="sphere" name="sphere" step=".01" required />

      <label htmlFor="cylinder">Cylinder</label>
      <input type="number" id="cylinder" name="cylinder" step=".01" required />

      <label htmlFor="unit_price">Unit Price</label>
      <input
        type="number"
        id="unit_price"
        name="unit_price"
        pattern="\d*\.?\d*"
        step=".01"
        required
      />

      <label htmlFor="quantity">Quantity</label>
      <input type="number" id="quantity" name="quantity" />

      <label htmlFor="storage_limit">Storage Limit</label>
      <input type="number" id="storage_limit" name="storage_limit" />

      <label htmlFor="comment">Comment</label>
      <textarea id="comment" name="comment" />

      {mutation.isSuccess && <span>successfully submitted!</span>}
      <button type="submit">Submit</button>
    </form>
  );
};
