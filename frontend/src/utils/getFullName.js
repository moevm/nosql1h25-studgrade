export default function getFullName(user) {
  if (!user) return "";
  const { lastName, firstName, middleName } = user;
  return `${lastName || ""} ${firstName || ""} ${middleName || ""}`.trim();
}
