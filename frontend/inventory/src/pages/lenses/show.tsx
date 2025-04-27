import { useOne } from "@refinedev/core";

export const LensShow = () => {
  const { data, isLoading } = useOne({ resource: "lenses", id: 1 });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      Lens: {data?.data.id}, {data?.data.lens_type}, {data?.data.sphere},{" "}
      {data?.data.cylinder}
    </div>
  );
};
