import { useShow } from "@refinedev/core";

export const LensShow = () => {
  const {
    query: { data, isLoading },
  } = useShow();

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
